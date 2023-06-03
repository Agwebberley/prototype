// Load the base.html file
fetch('base.html')
    .then(response => response.text())
    .then(data => {
        // Split the code at the {% block content %} tag
        const parts = data.split('{% block content %} {% endblock %}');
        
        // Split the head and body code
        const head = parts[0].split('<body class="bg-white dark:bg-gray-900"> ')[0];
        const body = parts[0].split('<body class="bg-white dark:bg-gray-900"> ')[1];
        
            console.log(head);
        // Insert the head and tail code into the index.html file
        document.head.insertAdjacentHTML('afterbegin', head);
        document.body.innerHTML = body + document.body.innerHTML + parts[1];
    });