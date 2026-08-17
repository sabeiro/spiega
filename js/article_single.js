document.addEventListener('DOMContentLoaded', () => {
    // ✅ Markdown conversion
    document.getElementById('blog-content').innerHTML = marked.parse(document.querySelector('#blog-markdown').textContent);

    // ✅ Collapsible code/details
    const collapsible = document.querySelectorAll('details code, pre, blockquote, img[alt*=Figure]');

    const sections = document.getElementById('blog-content');
    sections.querySelectorAll('.markdown-section').forEach(function(section) {
	if (section.classList.contains('expandable')) {
	    const summary = document.createElement('details');
	    const heading = document.createElement('summary');
	    heading.innerText = '';
	    // Optional header or description logic goes here
	    let textContent = '';

	    if (section.previousElementSibling) {
		const textNode = [...section.previousElementSibling.childNodes].find(node => node.nodeValue.trim().length > 0);
		if (textNode) {
		    heading.innerText = '[Click to Expand] Section';
		}
	    }
	    
	    summary.appendChild(heading);
	    summary.appendChild(section);

	    document.getElementById('blog-content').prepend(summary);
	}
    });
});

function toggleMenu() {
    const menu = document.querySelector('.nav-menu');
    const icon = document.querySelector('.hamburger .bar:nth-of-type(1)');
    menu.classList.toggle('mobile-active');
    
    // If we want the 'X' close animation
    const closeMenu = () => {
	menu.classList.remove('mobile-active');
	icon.style.width = '24px';
    };
}
