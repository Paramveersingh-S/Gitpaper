import Head from 'next/head';
import Link from 'next/link';

export default function RepoView() {
  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Head>
        <title>Repo Details - GitPaper</title>
      </Head>

      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/dashboard" className="text-gray-500 hover:text-gray-900">
              ← Back
            </Link>
            <div className="h-6 w-px bg-gray-300"></div>
            <h1 className="font-bold text-xl text-gray-900 flex items-center">
              Paramveersingh-S / llm-training-framework
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <div className="mb-10">
          <h2 className="text-lg font-bold text-gray-900 mb-4">Linked Papers</h2>
          
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 mb-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-semibold text-gray-900">Attention Is All You Need</h3>
                <p className="text-sm text-gray-500 mt-1">Vaswani et al., 2017 • arXiv:1706.03762</p>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full">
                85% Coverage
              </span>
            </div>
            
            <p className="text-sm text-gray-700 mb-6 max-w-3xl line-clamp-2">
              The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms...
            </p>
            
            <h4 className="text-sm font-semibold text-gray-900 mb-3 border-b pb-2">Equation Mapping</h4>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 text-sm">
                <thead>
                  <tr>
                    <th className="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider rounded-tl-lg">Equation</th>
                    <th className="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                    <th className="px-4 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider rounded-tr-lg">Implementation File</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  <tr>
                    <td className="px-4 py-3 whitespace-nowrap font-mono text-gray-900">eq:1</td>
                    <td className="px-4 py-3 whitespace-nowrap"><span className="text-green-500">✅ Implemented</span></td>
                    <td className="px-4 py-3 whitespace-nowrap text-gray-600 font-mono text-xs">models/attention.py</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 whitespace-nowrap font-mono text-gray-900">eq:2</td>
                    <td className="px-4 py-3 whitespace-nowrap"><span className="text-green-500">✅ Implemented</span></td>
                    <td className="px-4 py-3 whitespace-nowrap text-gray-600 font-mono text-xs">models/attention.py</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 whitespace-nowrap font-mono text-gray-900">algo:1</td>
                    <td className="px-4 py-3 whitespace-nowrap"><span className="text-red-500">❌ Missing</span></td>
                    <td className="px-4 py-3 whitespace-nowrap text-gray-400 italic">Not found in commits</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-lg font-bold text-gray-900 mb-4">Recent Drift Warnings</h2>
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-md">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">Warning on PR #42</h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <p>Modified <code>models/attention.py</code> which implements [eq:1] from Attention Is All You Need.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </main>
    </div>
  );
}
