var NexT = window.NexT || {};
var CONFIG = {
  root: '/',
  scheme: 'Mist',
  sidebar: {"position":"right","display":"post"},
  fancybox: true,
  motion: true,
  duoshuo: {
    userId: 'undefined',
    author: '博主'
  },
  algolia: {
    applicationID: '',
    apiKey: '',
    indexName: '',
    hits: {"per_page":10},
    labels: {"input_placeholder":"Search for Posts","hits_empty":"We didn't find any results for the search: ${query}","hits_stats":"${hits} results found in ${time} ms"}
  }
};