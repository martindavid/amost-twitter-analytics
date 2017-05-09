function (doc) {
    if (doc.coordinates && doc.coordinates !== null) {
        var parsedDate = new Date(doc.created_at);
        var formattedDate = parsedDate.getFullYear() + "/" + parsedDate.getMonth() + "/" + parsedDate.getDate();
        var coordinates = doc.coordinates.coordinates;
        if ((coordinates[0] >= 139.654083252 && coordinates[0] <= 149.0885925293) 
            && (coordinates[1] >= -38.548165423 && coordinates[1] <= -34.1436348203)) {
            emit(formattedDate, 1);
        }
    }
}