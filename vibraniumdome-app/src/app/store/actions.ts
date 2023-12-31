//@ts-ignore
export const addInputShield = (item) => ({
 type: 'ADD_INPUT_SHIELD',
 payload: item,
});
//@ts-ignore
export const removeInputShield = (item) => ({
 type: 'REMOVE_INPUT_SHIELD',
 payload: item,
});
//@ts-ignore
export const setInputShield = (items: any[]) => ({
 type: 'SET_INPUT_SHIELD',
 payload: items,
});
export const resetInputShield = () => ({
 type: 'RESET_INPUT_SHIELD',
});
//@ts-ignore
export const addOutputShield = (item) => ({
 type: 'ADD_OUTPUT_SHIELD',
 payload: item,
});
//@ts-ignore
export const setOutputShield = (items: any[]) => ({
 type: 'SET_OUTPUT_SHIELD',
 payload: items,
});
//@ts-ignore
export const removeOutputShield = (item) => ({
 type: 'REMOVE_OUTPUT_SHIELD',
 payload: item,
});
export const resetOutputShield = () => ({
 type: 'RESET_OUTPUT_SHIELD',
});