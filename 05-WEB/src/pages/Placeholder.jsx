export default function Placeholder({ title, Icon }) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-10">
      {Icon && <Icon size={56} className="mx-auto mb-4 text-muted opacity-20" />}
      <h2 className="text-xl font-bold text-text mb-2">{title}</h2>
      <p className="text-sm text-muted max-w-sm">
        Esta página está em desenvolvimento. Acesse{' '}
        <strong>Predições</strong> para ver a principal funcionalidade do sistema.
      </p>
    </div>
  )
}
