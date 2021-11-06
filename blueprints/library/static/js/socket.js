document.addEventListener('DOMContentLoaded', function(){
    var socket = io('/library');
    socket.on('library', function(json) {
        console.log('Received '+json.data.length+' elements.');
        console.log(json.data)

        options = {
            valueNames: ['id', 'name', 'description', 'needed_by', 'duration', 'borrower', 'lender' ],
            item: `
                <li class="item-expanded-row">
                    <div class="item-row row-main flex-horizontal">
                        <span class="id item"></span>
                        <span class="name item"></span>
                        <span class="description item"></span>
                        <span class="needed_by item"></span>
                    </div>
                    <div class="item-row row-details flex-horizontal">
                        <span class="duration item-detail"></span>
                        <span class="borrower item-detail"></span>
                        <span class="lender item-detail"></span>
                </li>
            `,
        };
        var itemList = new List('items', options);
        itemList.clear().add(json.data);
    });
});
