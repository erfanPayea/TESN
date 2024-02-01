def post_serializer(post, do_you_like_it):
    data = {
        'id': post.id,
        'sentTime': post.sent_time,
        'ownerId': post.owner.id,
        'ownerUsername': post.owner.username,
        'attraction': None,
        'numberOfLikes': post.number_of_likes,
        'caption': post.caption,
        'filePath': post.file_path,
        'doYouLikeIt': do_you_like_it
    }

    if post.attraction is not None:
        data["attraction"] = post.attraction.id

    return data


def review_serializer(review, do_you_like_it):
    return {
        'id': review.id,
        'sentTime': review.sent_time,
        'ownerId': review.owner.id,
        'ownerUsername': review.owner.username,
        'attraction': attraction_serializer(review.attraction),
        'rating': review.rating,
        'numberOfLikes': review.number_of_likes,
        'caption': review.caption,
        'filePath': review.file_path,
        'doYouLikeIt': do_you_like_it
    }


def comment_serializer(comment, do_you_like_it):
    return {
        'id': comment.id,
        'message': comment.message,
        'sentTime': comment.sent_time,
        'ownerId': comment.owner.id,
        'ownerUsername': comment.owner.username,
        'numberOfLikes': comment.number_of_likes,
        'doYouLikeIt': do_you_like_it
    }


def attraction_serializer(attraction):
    return {

    }
