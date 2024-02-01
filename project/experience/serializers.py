def post_serializer(post, do_you_like_it, best_comment_message):
    data = {
        'id': post.id,
        'sentTime': post.sent_time,
        'owner': post.owner.id,
        'attraction': None,
        'numberOfLikes': post.number_of_likes,
        'caption': post.caption,
        'filePath': post.file_path,
        'doYouLikeIt': do_you_like_it,
        'bestCommentMessage': best_comment_message
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
        'rating': review.rating,
        'numberOfLikes': review.number_of_likes,
        'caption': review.caption,
        'filePath': review.file_path,
        'doYouLikeIt': do_you_like_it
    }


def comment_serializer(comment, do_you_like_it):
    if comment == -1:
        return "No comment yet!"
    return {
        'id': comment.id,
        'message': comment.message,
        'sentTime': comment.sent_time,
        'owner': comment.owner,
        'numberOfLikes': comment.number_of_likes,
        'doYouLikeIt': do_you_like_it
    }
