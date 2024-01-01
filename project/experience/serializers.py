def post_serializer(post):
    data = {
        'id': post.id,
        'sent_time': post.sent_time,
        'owner': post.owner.id,
        'attraction': None,
        'number_of_likes': post.number_of_likes,
        'caption': post.caption,
        'file_path': post.file_path
    }

    if post.attraction is not None:
        data["attraction"] = post.attraction.id

    return data


def review_serializer(review):
    return {
        'id': review.id,
        'sent_time': review.sent_time,
        'owner': review.owner.id,
        'attraction': review.attraction.id,
        'number_of_likes': review.number_of_likes,
        'caption': review.caption,
        'file_path': review.file_path
    }


def comment_serializer(comment):
    return {
        'id': comment.id,
        'sent_time': comment.sent_time,
        'owner': comment.owner,
        'number_of_likes': comment.number_of_likes
    }
