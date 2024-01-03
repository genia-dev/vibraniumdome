'use client'

import { Provider } from 'jotai'

//@ts-ignore
export default function Providers({ children }) {
  return (
    <Provider>
      {children}
    </Provider>
  )
}