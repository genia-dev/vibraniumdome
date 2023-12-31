//@ts-ignore
const initialState = [];

//@ts-ignore
function outputShieldsReducer(state = initialState, action) {
  switch (action.type) {
    case 'ADD_OUTPUT_SHIELD':
      return [...state, action.payload];
    case 'REMOVE_OUTPUT_SHIELD':
      return state.filter(item => item.id !== action.payload);
    case 'RESET_OUTPUT_SHIELD':
      //@ts-ignore
      return initialState;
    case 'SET_OUTPUT_SHIELD':
      state.splice(0, state.length);
      state.push(...action.payload);
    default:
      return state;
  }
}

export default outputShieldsReducer;