def post_serializer(post, do_you_like_it):
    data = {
        'id': post.id,
        'sentTime': post.sent_time,
        'owner': post.owner.id,
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
        'owner': review.owner.id,
        'attraction': review.attraction.id,
        'numberOfLikes': review.number_of_likes,
        'caption': review.caption,
        'filePath': review.file_path,
        'doYouLikeIt': do_you_like_it
    }


def comment_serializer(comment, do_you_like_it):
    return {
        'id': comment.id,
        'sentTime': comment.sent_time,
        'owner': comment.owner,
        'numberOfLikes': comment.number_of_likes,
        'doYouLikeIt': do_you_like_it
    }
