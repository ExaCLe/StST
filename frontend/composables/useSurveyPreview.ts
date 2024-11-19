import { useIndexedDB } from './useIndexedDB';

export const useSurveyPreview = () => {
  const { setData, getData, deleteData } = useIndexedDB();
  const CHUNK_SIZE = 1024 * 1024; // 1MB chunks
  const PREVIEW_KEY = 'surveyPreview';

  // Helper to split data into chunks
  const splitIntoChunks = (data: string): string[] => {
    const chunks: string[] = [];
    for (let i = 0; i < data.length; i += CHUNK_SIZE) {
      chunks.push(data.slice(i, i + CHUNK_SIZE));
    }
    return chunks;
  };

  // Helper to store chunked data
  const storeChunkedData = async (key: string, data: any) => {
    const serialized = JSON.stringify(data);
    const chunks = splitIntoChunks(serialized);
    
    // Store metadata
    await setData(`${key}_meta`, {
      chunks: chunks.length,
      timestamp: Date.now()
    });

    // Store chunks
    for (let i = 0; i < chunks.length; i++) {
      await setData(`${key}_chunk_${i}`, chunks[i]);
    }
  };

  // Helper to retrieve chunked data
  const getChunkedData = async (key: string) => {
    try {
      const meta = await getData(`${key}_meta`);
      if (!meta) return null;

      const chunks: string[] = [];
      for (let i = 0; i < meta.chunks; i++) {
        const chunk = await getData(`${key}_chunk_${i}`);
        if (!chunk) throw new Error('Chunk missing');
        chunks.push(chunk);
      }

      return JSON.parse(chunks.join(''));
    } catch (e) {
      console.error('Error retrieving chunked data:', e);
      return null;
    }
  };

  // Helper to clear chunked data
  const clearChunkedData = async (key: string) => {
    try {
      const meta = await getData(`${key}_meta`);
      if (meta) {
        for (let i = 0; i < meta.chunks; i++) {
          await deleteData(`${key}_chunk_${i}`);
        }
        await deleteData(`${key}_meta`);
      }
    } catch (e) {
      console.error('Error clearing chunked data:', e);
    }
  };

  const openPreview = async (surveyData: any) => {
    try {
      await storeChunkedData(PREVIEW_KEY, surveyData);
      const previewUrl = `/preview-survey`;
      window.open(previewUrl, '_blank');
    } catch (e) {
      console.error('Error storing preview data:', e);
    }
  };

  const getPreviewData = async () => {
    try {
      return await getChunkedData(PREVIEW_KEY);
    } catch (e) {
      console.error('Error reading preview data:', e);
      return null;
    }
  };

  const clearPreviewData = async () => {
    try {
      await clearChunkedData(PREVIEW_KEY);
    } catch (e) {
      console.error('Error clearing preview data:', e);
    }
  };

  return {
    openPreview,
    getPreviewData,
    clearPreviewData
  };
};
