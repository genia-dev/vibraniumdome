import { atom } from 'jotai'

export const policyNameAtom = atom('')
export const llmAppAtom = atom('')
export const lowRiskThresholdAtom = atom(undefined)
export const highRiskThresholdAtom = atom(undefined)
export const shieldsFilterAtom = atom('')
export const redactConversationAtom = atom('')
export const inputShieldsAtom = atom([])
export const outputShieldsAtom = atom([])
export const lastShieldAtom = atom('')