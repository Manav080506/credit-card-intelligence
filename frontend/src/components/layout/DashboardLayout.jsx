function DashboardLayout({ sidebar, children }) {
  return (
    <section className="min-h-screen bg-[#020617] text-slate-200">
      <div className="flex min-h-screen">
        <aside className="hidden h-screen w-[240px] shrink-0 border-r border-slate-800 bg-slate-950/40 p-4 xl:block">
          {sidebar}
        </aside>
        <main className="min-w-0 flex-1 overflow-y-auto">
          <div className="mx-auto flex w-full max-w-[1280px] flex-col space-y-6 px-6 py-6">
            <div className="xl:hidden">{sidebar}</div>
            {children}
          </div>
        </main>
      </div>
    </section>
  )
}

export default DashboardLayout
