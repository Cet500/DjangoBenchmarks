document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.custom-slider').forEach(slider => {
        initSlider(slider);
    });
});

function initSlider(slider) {
    const wrapper = slider.parentElement;
    const label = wrapper.querySelector('label');
    const id = slider.id;

    const valueDisplay = document.createElement('span');
    valueDisplay.className = 'slider-value';
    valueDisplay.id = `${id}-value`;
    valueDisplay.textContent = slider.value;

    const header = document.createElement('div');
    header.className = 'slider-header';
    header.appendChild(label.cloneNode(true));
    header.appendChild(valueDisplay);

    const container = document.createElement('div');
    container.className = 'slider-container';

    const track = document.createElement('div');
    track.className = 'slider-track';

    const fill = document.createElement('div');
    fill.className = 'slider-fill';

    // Добавляем классы для цветов и zebra-эффекта
    if (slider.classList.contains('good')) fill.classList.add('good');
    if (slider.classList.contains('warning')) fill.classList.add('warning');
    if (slider.classList.contains('bad')) fill.classList.add('bad');
    if (slider.classList.contains('zebra')) fill.classList.add('zebra');

    track.appendChild(fill);
    container.appendChild(track);
    container.appendChild(slider);

    wrapper.innerHTML = '';
    wrapper.appendChild(header);
    wrapper.appendChild(container);

    function updateSlider() {
        const min = parseFloat(slider.min);
        const max = parseFloat(slider.max);
        const value = parseFloat(slider.value);
        const thumbSize = 24;
        const trackWidth = slider.offsetWidth;
        const percent = (value - min) / (max - min);
        const fillWidth = percent * (trackWidth - thumbSize) + thumbSize / 2;

        fill.style.width = `${fillWidth}px`;
        valueDisplay.textContent = value;
    }

    slider.addEventListener('input', updateSlider);
    window.addEventListener('resize', updateSlider);
    updateSlider();
}
