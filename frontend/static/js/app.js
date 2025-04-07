// Функция для отображения уведомлений с использованием классов Bootstrap
function showAlert(type, message) {
    const container = document.createElement('div');
    container.classList.add('alert', `alert-${type}`, 'mt-3');
    container.role = 'alert';
    container.innerHTML = message;
    
    const existingAlerts = document.querySelector('.alert-container') || document.body;
    existingAlerts.appendChild(container);

    setTimeout(() => container.remove(), 30000); // Автоматическое исчезновение через 30 секунд
}

document.addEventListener("DOMContentLoaded", () => {
    const createButton = document.getElementById("create-secret-button");
    const readButton = document.getElementById("read-secret-button");
    const deleteButton = document.getElementById("delete-secret-button");

    const createModal = new bootstrap.Modal(document.getElementById("create-modal"));
    const readModal = new bootstrap.Modal(document.getElementById("read-modal"));
    const deleteModal = new bootstrap.Modal(document.getElementById("delete-modal"));

    // Открытие модальных окон
    createButton.addEventListener("click", () => createModal.show());
    readButton.addEventListener("click", () => readModal.show());
    deleteButton.addEventListener("click", () => deleteModal.show());

    // Логика для создания секрета
    const createForm = document.getElementById("create-secret-form");
    createForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const secretText = document.getElementById("secret-text").value;
        const ttl = document.getElementById("ttl").value;

        try {
            const response = await fetch(`${window.location.origin}:8000/api/v1/add_secret`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'pragma': 'no-cache',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Expires': 0
                },
                body: JSON.stringify({ secret: secretText, ttl_seconds: parseInt(ttl) })
            });

            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}: ${await response.text()}`);
            }

            const { key } = await response.json();
            showAlert('success', `Ваш ключ для доступа: ${key}`);
            createModal.hide(); // Скрыть модальное окно после успешной отправки
        } catch (error) {
            console.error("Ошибка создания секрета:", error.message);
            showAlert('danger', `Произошла ошибка при создании секрета.\n\nDetails:\n${error.message}`);
        }
    });

    // Логика для получения секрета
    const readForm = document.getElementById("read-secret-form");
    readForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const key = document.getElementById("key").value;

        try {
            const response = await fetch(`${window.location.origin}:8000/api/v1/get_secret/${encodeURIComponent(key)}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    'pragma': 'no-cache',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Expires': 0
                }
            });

            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error(`Секрет не найден.`);
                } else {
                    throw new Error(`Request failed with status ${response.status}: ${await response.text().trim()}`);
                }
            }

            const { secret } = await response.json();
            showAlert('info', secret); // Показать секрет в алерте
            readModal.hide(); // Скрыть модальное окно после успешной отправки
        } catch (error) {
            console.error("Ошибка чтения секрета:", error.message);
            showAlert('danger', `Не удалось получить секрет.\n\nDetails:\n${error.message}`);
        }
    });

    // Логика для удаления секрета
    const deleteForm = document.getElementById("delete-secret-form");
    deleteForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const key = document.getElementById("key").value;

        try {
            const response = await fetch(`${window.location.origin}:8000/api/v1/delete_secret/${encodeURIComponent(key)}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    'pragma': 'no-cache',
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Expires': 0
                }
            });

            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error(`Секрет не найден.`);
                } else {
                    throw new Error(`Request failed with status ${response.status}: ${await response.text().trim()}`);
                }
            }

            showAlert('success', "Секрет успешно удалён.");
            deleteModal.hide(); // Скрыть модальное окно после успешной отправки
        } catch (error) {
            console.error("Ошибка удаления секрета:", error.message);
            showAlert('danger', `Не удалось удалить секрет.\n\nDetails:\n${error.message}`);
        }
    });
});