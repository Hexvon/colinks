document.getElementById('linkForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const sourceLink = document.getElementById('sourceLink').value;

    try {
        const response = await fetch('https://colinks.onrender.com/api/links/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source_link: sourceLink })
        });

        if (!response.ok) {
            throw new Error('Не удалось создать короткую ссылку');
        }

        const data = await response.json();
        alert(`Короткая ссылка создана: ${data.short_link}`);
    } catch (error) {
        console.error(error);
        alert('Ошибка при создании короткой ссылки');
    }
});

document.getElementById('redirectForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const shortLink = document.getElementById('shortLink').value;

    try {
        const url = `https://colinks.onrender.com/api/${shortLink}`;

        window.location.href = url;
    } catch (error) {
        console.error(error);
        alert('Ошибка при переходе по короткой ссылке');
    }
});