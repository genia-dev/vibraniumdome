//@ts-ignore
const initialState = [];

//@ts-ignore
function inputShieldsReducer(state = initialState, action) {
  switch (action.type) {
    case 'ADD_INPUT_SHIELD':
      return [...state, action.payload];
    case 'REMOVE_INPUT_SHIELD':
      return state.filter(item => item.id !== action.payload);
    case 'RESET_INPUT_SHIELD':
      //@ts-ignore
      return initialState;
    case 'SET_INPUT_SHIELD':
      state.splice(0, state.length);
      state.push(...action.payload);
    default:
      return state;
  }
}

export default inputShieldsReducer;