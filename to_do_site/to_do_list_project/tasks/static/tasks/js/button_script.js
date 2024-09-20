document.addEventListener('DOMContentLoaded', function() {
    // Функция для обновления имени файла
    function updateFileName(input) {
        var fileName = input.files[0] ? input.files[0].name : "Файл не выбран";
        document.getElementById('file-name').textContent = fileName;
    }

    // Назначение функции полю выбора файла
    document.getElementById('profile_image').addEventListener('change', function() {
        updateFileName(this);
    });
});
