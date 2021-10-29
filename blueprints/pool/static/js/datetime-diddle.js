setDate = (obj, inFocus=true) => {
    if(inFocus) {
        obj.type = 'text';
        return;
    }

    today = new Date();
    cutoff = new Date();
    cutoff.setDate(today.getDate() + 7);

    obj.type = 'date';
    obj.min = today.toISOString().split('T')[0];
    obj.max = cutoff.toISOString().split('T')[0];
}
