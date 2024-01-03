import { atom } from 'jotai'

export const policyNameAtom = atom('')
export const llmAppAtom = atom('')
export const lowRiskThresholdAtom = atom(0.2)
export const highRiskThresholdAtom = atom(0.8)
export const shieldsFilterAtom = atom('all')
export const redactConversationAtom = atom(false)
export const inputShieldsAtom = atom([])
export const outputShieldsAtom = atom([])
export const lastShieldAtom = atom('')
export const lastShieldMetadataAtom = atom('{}')