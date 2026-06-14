export default function LoadingButton({ loading, children, className = '', ...props }) {
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      className={`${className} inline-flex items-center justify-center gap-3 rounded-full px-5 py-3 text-base font-semibold transition disabled:cursor-not-allowed disabled:opacity-60`}
    >
      {loading && (
        <span className="inline-flex h-5 w-5 animate-spin rounded-full border-2 border-white/10 border-t-white" />
      )}
      {children}
    </button>
  )
}
