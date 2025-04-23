export default function FormButton({ text, disabled, ...options }) {
  const className =
    "border border-violet-800 rounded px-4 py-2" +
    (disabled ? " bg-gray-400 italic cursor-not-allowed" : " hover:bg-lime-600 cursor-pointer");

  return (
    <button type="submit" className={className} disabled={disabled} {...options}>
      {text}
    </button>
  );
}