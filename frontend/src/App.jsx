// frontend/src/App.jsx
import { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

    // --- NEW: States for Q&A ---
  const [documentId, setDocumentId] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isAsking, setIsAsking] = useState(false);


  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setSummary('');
    setError('');
    setDocumentId(null);
    setAnswer('');
    setQuestion('');
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSummary('');
    setDocumentId(null);


    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/summarize/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSummary(response.data.summary);
    } catch (err) {
      setError('An error occurred. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
   // --- NEW: Function to handle the "Ask" button ---
  const handleAskSubmit = async () => {
    if (!question) {
      setError('Please enter a question.');
      return;
    }
    
    setIsAsking(true);
    setError('');
    setAnswer('');

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/ask/', {
        document_id: documentId,
        question: question,
      });
      setAnswer(response.data.answer);
    } catch (err) {
      setError('An error occurred while getting the answer.');
      console.error(err);
    } finally {
      setIsAsking(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">Document Summarizer & Q&A 📄</h1>
        
        <div className="mb-6">
          <label htmlFor="file-upload" className="block text-sm font-medium text-gray-700 mb-2">
            Upload your PDF document:
          </label>
          <input 
            id="file-upload" 
            type="file" 
            accept=".pdf"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={isLoading || !selectedFile}
          className="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition duration-300"
        >
          {isLoading ? 'Processing...' : 'Summarize'}
        </button>

        {error && <p className="text-red-500 text-center mt-4">{error}</p>}

        {summary && (
          <div className="mt-8 p-6 bg-gray-50 rounded-lg border border-gray-200">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Summary</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{summary}</p>

            {/* --- NEW: Q&A Section --- */}
            <div className="mt-6 border-t pt-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Ask a Question</h3>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask anything about the document..."
                  className="flex-grow border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
                <button
                  onClick={handleAskSubmit}
                  disabled={isAsking || !question}
                  className="bg-green-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {isAsking ? '...' : 'Ask'}
                </button>
              </div>

              {answer && (
                <div className="mt-4 p-4 bg-green-50 rounded-lg">
                   <p className="text-gray-800">{answer}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;