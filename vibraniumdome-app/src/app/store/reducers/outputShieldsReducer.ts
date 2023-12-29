//@ts-ignore
const initialState = [];

//@ts-ignore
function outputShieldsReducer(state = initialState, action) {
  switch (action.type) {
    case 'ADD_OUTPUT_SHIELD':
      return [...state, action.payload];
    case 'REMOVE_OUTPUT_SHIELD':
      return state.filter(item => item !== action.payload);
    case 'RESET_OUTPUT_SHIELD':
      //@ts-ignore
      return initialState;
    default:
      return state;
  }
}

export default outputShieldsReducer;