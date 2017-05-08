function (doc) {
    if (doc.coordinates && doc.coordinates !== null) {
        var parsedDate = new Date(doc.created_at);
        var formattedDate = parsedDate.getFullYear() + "/" + parsedDate.getMonth() + "/" + parsedDate.getDate();
        var text = doc.text.toLowerCase();

        coordinates = doc.coordinates.coordinates
        if ((coordinates[0] >= 139.654083252 && coordinates[0] <= 149.0885925293) 
            && (coordinates[1] >= -38.548165423 && coordinates[1] <= -34.1436348203)) {
            emit(formattedDate, {
                text: doc.text,
                lang: doc.lang,
                sentiment: doc.sentiment,
                coordinates: doc.coordinates.coordinates,
                user: {
                    id: doc.user.id,
                    name: doc.user.name,
                    profile_pic: doc.user.profile_image_url_https,
                    lang: doc.user.lang,
                    location: doc.user.location
                }
            });
        }
    }
}