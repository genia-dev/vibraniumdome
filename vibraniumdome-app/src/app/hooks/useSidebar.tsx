import { create } from "zustand";

interface SidebarStore {
    isOpen: boolean;
    toggle: () => void;
}

export const useSidebar = create<SidebarStore>((set) => ({
    // set the sidebar to be closed by default
    isOpen: false,
    toggle: () => set((state) => ({ isOpen: !state.isOpen })),
}));