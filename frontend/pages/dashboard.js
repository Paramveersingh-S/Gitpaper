import Head from 'next/head';
import Link from 'next/link';

export default function Dashboard() {
  const repos = [
    { id: 1, owner: "Paramveersingh-S", name: "llm-training-framework", coverage: 85, papers: 3 },
    { id: 2, owner: "Paramveersingh-S", name: "vision-transformer", coverage: 60, papers: 1 },
  ];

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Head>
        <title>Dashboard - GitPaper</title>
      </Head>

      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="font-bold text-xl text-gray-900 flex items-center">
            📐 GitPaper
          </Link>
          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium text-gray-700">@Paramveersingh-S</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Your Repositories</h1>
            <p className="text-gray-500 text-sm mt-1">Repositories with GitPaper installed</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {repos.map((repo) => (
            <Link href={`/repo/${repo.owner}/${repo.name}`} key={repo.id}>
              <div className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow p-6 flex flex-col h-full cursor-pointer">
                <h3 className="font-semibold text-lg text-gray-900 truncate">{repo.name}</h3>
                <p className="text-sm text-gray-500 mb-4">{repo.owner}</p>
                
                <div className="mt-auto">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-medium text-gray-600">Equation Coverage</span>
                    <span className="text-xs font-semibold text-gray-900">{repo.coverage}%</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2 mb-3">
                    <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${repo.coverage}%` }}></div>
                  </div>
                  
                  <div className="flex items-center text-xs text-gray-500">
                    <svg className="w-4 h-4 mr-1 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    {repo.papers} {repo.papers === 1 ? 'Paper' : 'Papers'} Linked
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
