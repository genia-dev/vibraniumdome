import logging
import os
from typing import List, Tuple

import yaml
from datasets import load_dataset
from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.azure_openai import AzureOpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from vibraniumdome_shields.utils import load_vibranium_home, uuid4_str


class VectorDBService:
    _logger = logging.getLogger(__name__)
    _vector_store: FAISS
    _embeddings = OpenAIEmbeddings

    def __init__(self, vector_db_dir, index_name, embedding_model_name):
        self.vector_store_file_path = os.path.join(vector_db_dir, "vibranium-vector-store", "data.faiss")
        self.vector_store_dir = os.path.join(vector_db_dir, "vibranium-vector-store")
        self._index_name = index_name
        self._vector_store = FAISS
        
        # Note: requires those env vars
        ####################################################################################
        # os.environ["AZURE_OPENAI_API_KEY"] = "..."
        # os.environ["AZURE_OPENAI_ENDPOINT"] = "https://<your-endpoint>.openai.azure.com/"

        if os.getenv("OPENAI_API_TYPE") == "azure":
            self._embeddings = AzureOpenAIEmbeddings(
                    azure_deployment=os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
                    openai_api_version=os.environ.get("AZURE_OPENAI_EMBEDDING_VERSION"),)
        else:
            self._embeddings = OpenAIEmbeddings(model=embedding_model_name)

        if os.path.exists(self.vector_store_file_path):
            self._vector_store = self._vector_store.load_local(folder_path=self.vector_store_dir, embeddings=self._embeddings, index_name=self._index_name)
        else:
            self.init_vector_store()
        self._logger.info("vectordb initialized")

    def init_vector_store(self):
        self._logger.debug("the vectordb collection is empty, start initializing")
        self._init_vector_with_local_prompt_injections()
        self._load_external_data()
        self._logger.debug("vectordb data loaded")

    def add_texts(self, texts: List[str]):
        length = len(texts)
        self._logger.debug("Adding %d texts", length)
        try:
            ids = [uuid4_str() for _ in range(length)]
            self._vector_store.add_texts(texts=texts, ids=ids)
            return ids
        except Exception as err:
            self._logger.exception("exception while adding text to collection")
            raise err

    def add_embeddings(self, texts: List[str], embeddings: List[List], metadatas: List[dict]):
        length = len(texts)
        self._logger.debug("Adding %d text embeddings", length)
        try:
            ids = [uuid4_str() for _ in range(length)]
            self._vector_store.add_embeddings(texts=texts, text_embeddings=embeddings, metadatas=metadatas, ids=ids)
            return ids
        except Exception as err:
            self._logger.exception("exception while adding embeddings to collection")
            raise err

    def query(self, text: str, k: int = 3) -> List[Tuple[Document, float]]:
        self._logger.debug("vectordb query: %s %s", text, k)
        try:
            return self._vector_store.similarity_search_with_score(text, k)
        except Exception as e:
            self._logger.exception("exception while query vectordb: %s", text)
            raise e

    def _load_file(self, dataset_path: str, type: str):
        # Load the dataset using the load_dataset function
        return load_dataset(type, data_files=dataset_path)

    def _load_parquet_file(self, path):
        dataset = self._load_file(path, "parquet")
        self._logger.info("path: %s loaded with %s", path, dataset.shape["train"])
        return dataset

    def _init_vector_with_local_prompt_injections(self):
        vibranium_home = load_vibranium_home()
        full_path = os.path.join(vibranium_home, "vibraniumdome_shields", "prompt-injections.yaml")
        data = None
        with open(full_path, "r") as f:
            data = yaml.safe_load(f)

        self._vector_store = self._vector_store.from_texts(texts=data["prompts"], embedding=self._embeddings)

    def _load_hf_jasper(self):
        dataset = self._load_parquet_file(
            "https://huggingface.co/datasets/JasperLS/prompt-injections/resolve/main/data/train-00000-of-00001-9564e8b05b4757ab.parquet"
        )
        ds = dataset.filter(lambda example: example["label"] == 1)
        self.add_texts(ds["train"]["text"])

    def _load_hf_gandalf(self):
        dataset = self._load_parquet_file(
            "https://huggingface.co/datasets/Lakera/gandalf_ignore_instructions/resolve/main/data/train-00000-of-00001-ded53be747ff55cd.parquet"
        )
        self.add_texts(dataset["train"]["text"])

    def _load_GPT_Fuzz(self):
        dataset = self._load_file("https://raw.githubusercontent.com/sherdencooper/GPTFuzz/master/datasets/prompts/GPTFuzzer.csv", "csv")
        # dataset = self._load_file("https://raw.githubusercontent.com/sherdencooper/GPTFuzz/master/datasets/questions/question_list.csv", "csv")
        self.add_texts(dataset["train"]["text"])

    def _load_external_data(self):
        self._load_hf_gandalf()
        self._load_GPT_Fuzz()
        self._load_hf_jasper()
        self._vector_store.save_local(self.vector_store_dir, index_name=self._index_name)
