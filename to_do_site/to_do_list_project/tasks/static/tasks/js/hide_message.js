document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript загружен и DOMContentLoaded сработал');

    // Ищем элементы с классом alert вместо alert-dismissible
    const messages = document.querySelectorAll('.alert');
    console.log('Найденные сообщения:', messages);

    messages.forEach(function(message) {
        console.log('Обрабатываем сообщение:', message);
        setTimeout(function() {
            message.classList.add('fade');
            message.style.opacity = '0';
        }, 5000);
    });
});
