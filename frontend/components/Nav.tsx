export default function Nav() {
  return (
    <header className="border-b bg-white">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <a href="/" className="font-bold">AI Resume CoPilot</a>
        <nav className="flex gap-4 text-sm">
          <a className="hover:underline" href="/resume">Resume</a>
          <a className="hover:underline" href="/jobs">Match</a>
          <a className="hover:underline" href="/learning">Learning</a>
          <a className="hover:underline" href="/dashboard">Dashboard</a>
        </nav>
      </div>
    </header>
  );
}
