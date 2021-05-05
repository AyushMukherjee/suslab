document.addEventListener('DOMContentLoaded', function () {
    const appComponents = document.querySelectorAll('.app-component');

    let active = -1;

    function uncover(key) {
        console.log(key);
        console.log(active);
        if(active !== -1)
            appComponents[active].querySelector('.app-icon').classList.remove('app-select');
        if(key === active)
        {
            active = -1;
            return;
        }

        active = key;
        appComponents[key].querySelector('.app-icon').classList.add('app-select');
    }

    appComponents.forEach((component, key) => {
        component.addEventListener('click', () => uncover(key))
    })
});
