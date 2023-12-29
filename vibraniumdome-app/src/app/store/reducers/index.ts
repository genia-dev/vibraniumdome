// store/reducers/index.ts
import { combineReducers } from 'redux';
import inputShieldsReducer from './inputShieldsReducer';
import outputShieldsReducer from './outputShieldsReducer';

export const rootReducer = combineReducers({
  inputShields: inputShieldsReducer,
  outputShields: outputShieldsReducer,
});