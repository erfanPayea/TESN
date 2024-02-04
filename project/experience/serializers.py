from . import models


def post_serializer(user, post, do_you_like_it):
    all_comments = post.comments.all().order_by('-number_of_likes')
    if len(all_comments) > 0:
        like_comment = models.LikeComment.objects.filter(owner=user, destination_comment=all_comments[0]).first()
        best_comment = comment_serializer(all_comments[0], like_comment is not None)
    else:
        best_comment = {
            'id': -1,
            'ownerUsername': 'Host',
            'ownerId': '0',
            'ownerAvatarPath': None,
            'message': 'No comments yet!',
            'numberOfLikes': '0'
        }
    data = {
        'id': post.id,
        'sentTime': post.sent_time,
        'ownerId': post.owner.id,
        'ownerUsername': post.owner.username,
        'ownerAvatarPath': "http://127.0.0.1:8000/media/" + str(post.owner.avatar_image),
        'attractionId': None,
        'attractionName': 'No attraction is targeted!',
        'numberOfLikes': post.number_of_likes,
        'caption': post.caption,
        'image': "http://127.0.0.1:8000/media/" + str(post.image),
        'doYouLikeIt': do_you_like_it,
        'bestComment': best_comment,
    }

    if post.attraction is not None:
        data["attractionId"] = post.attraction.id
        data['attractionName'] = post.attraction.name

    return data


def review_serializer(review, do_you_like_it):
    return {
        'id': review.id,
        'sentTime': review.sent_time,
        'ownerId': review.owner.id,
        'ownerUsername': review.owner.username,
        'ownerAvatarPath': "http://127.0.0.1:8000/media/" + str(review.owner.avatar_image),
        'attractionId': review.attraction.id,
        'attractionName': review.attraction.name,
        'rating': review.rating,
        'numberOfLikes': review.number_of_likes,
        'caption': review.caption,
        'doYouLikeIt': do_you_like_it
    }


def comment_serializer(comment, do_you_like_it):
    return {
        'id': comment.id,
        'message': comment.message,
        'sentTime': comment.sent_time,
        'ownerId': comment.owner.id,
        'ownerUsername': comment.owner.username,
        'ownerAvatarPath': "http://127.0.0.1:8000/media/" + str(comment.owner.avatar_image),
        'numberOfLikes': comment.number_of_likes,
        'doYouLikeIt': do_you_like_it
    }


def attraction_serializer(attraction):
    return {
        'id': attraction.id,
        'name': attraction.name
    }
