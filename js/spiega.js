hljs.initHighlightingOnLoad();
var link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = window.location.search.match(/print-pdf/gi) ? 'css/pdf.css' : 'css/modest.css';
document.getElementsByTagName('head')[0].appendChild(link);
MathJax.Hub.Config({
    tex2jax: {
	inlineMath: [ ['$','$'], ["\\(","\\)"] ],
	processEscapes: true
    }
    // ,tex: {physics: {italicdiff: false,arrowdel: false }}
    ,tex: {packages: {'[+]': ['physics']}}
});
