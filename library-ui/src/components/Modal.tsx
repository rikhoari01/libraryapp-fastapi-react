import * as Dialog from "@radix-ui/react-dialog";

interface ModalProps {
    title: string;
    children: React.ReactNode;
    open: boolean;
    onOpenChange: (open: boolean) => void;
}

export default function Modal({ title, children, open, onOpenChange }: ModalProps) {
    return (
        <Dialog.Root open={open} onOpenChange={onOpenChange}>
            <Dialog.Portal>
                <Dialog.Overlay className="fixed inset-0 bg-black/50" />
                <Dialog.Content className="fixed top-1/2 left-1/2 w-[400px] -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl p-6 shadow-lg">
                    <Dialog.Title className="text-lg font-bold mb-4">{title}</Dialog.Title>
                    {children}
                    <Dialog.Close asChild>
                        <button className="mt-4 px-3 py-1 rounded bg-gray-200 hover:bg-gray-300">Close</button>
                    </Dialog.Close>
                </Dialog.Content>
            </Dialog.Portal>
        </Dialog.Root>
    );
}
