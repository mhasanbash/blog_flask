fetch('http://127.0.0.1:5000/objects/count')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const count = data;
        document.getElementById('count').innerHTML = count;
    })
    .catch(error => {
        console.error('خطا در دریافت تعداد اشیاء:', error);
    });
