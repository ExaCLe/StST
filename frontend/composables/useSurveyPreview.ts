export const useSurveyPreview = () => {
  const openPreview = (surveyData: any) => {
    console.log('Survey data:', surveyData);
    // Store the preview data in localStorage
    localStorage.setItem('surveyPreview', JSON.stringify(surveyData));
    
    // Open new tab with preview
    const previewUrl = `/preview-survey`;
    window.open(previewUrl, '_blank');
  };

  const getPreviewData = () => {
    try {
      const data = localStorage.getItem('surveyPreview');
      return data ? JSON.parse(data) : null;
    } catch (e) {
      console.error('Error reading preview data:', e);
      return null;
    }
  };

  const clearPreviewData = () => {
    localStorage.removeItem('surveyPreview');
  };

  return {
    openPreview,
    getPreviewData,
    clearPreviewData
  };
};
