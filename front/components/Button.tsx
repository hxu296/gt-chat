export function Button({ ...props }: any) {
  return (
    <button
      className="inline-flex items-center justify-center gap-2 rounded-md bg-zinc-600 py-2 px-3 text-sm font-semibold text-zinc-100 outline-offset-2 transition hover:bg-zinc-400 active:bg-zinc-800 active:text-zinc-100/70 active:transition-none"
      {...props}
    />
  );
}
