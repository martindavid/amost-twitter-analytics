function (doc) {
    if (!doc.retweet_status && doc.coordinates) {
        var parsedDate = new Date(doc.created_at);
        var formattedDate = parsedDate.getFullYear() + "/" + parsedDate.getMonth() + "/" + parsedDate.getDate() + " " + parsedDate.getHours() + ":" + parsedDate.getMinutes() + ":" + parsedDate.getSeconds();
        var text = doc.text.toLowerCase();
        if (text.indexOf('shop') !== -1 || text.indexOf('shopping') !== -1 || text.indexOf('mall') !== -1
            || doc.indexOf('hangout')) {
            emit(formattedDate, {
                text: doc.text,
                lang: doc.lang,
                coordinates: doc.coordinates,
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