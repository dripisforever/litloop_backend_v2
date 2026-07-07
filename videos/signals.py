from django.db.models.signals import post_save
from django.dispatch import receiver
from videos.models import Video, VideoComment
from comments.models import Comment


FAKE_COMMENTS = [
    {
        'text': '“The best place to hide is in plain sight.”– Edgar Allan Poe, (The Purloined Letter)',
        'replies': [
            {
                'text': 'I had to read that short story for a sociology seminar. Pretty good read!',
                'replies': [
                    {
                        'text': 'I read it in 6th grade because it was one of the highest "reading level" books while not being forever long. I passed the comprehension test to my teachers delight and I found Edgar Allan Poe.',
                        'replies': [],
                    },
                ],
            },
        ],
    },
    {
        'text': 'How is this possible?.',
        'replies': [
            {
                'text': "OP's title is inaccurate, that's why.\n\nEscobar did not become wanted in the United States until the late 1980s. He wouldn't have had any restrictions traveling to and around the US in 1981.",
                'replies': [
                    {
                        'text': 'BREAK OUT THE PITCHFORKS, STAT!',
                        'replies': [],
                    },
                ],
            },
        ],
    },
    {
        'text': "He wasn't that notable to the US when this picture was taken",
        'replies': [
            {
                'text': "Although he was a criminal by 1981, he wasn't even wanted in Colombia at that time, much less the U.S.",
                'replies': [
                    {
                        'text': 'Poor guy nobody wanted him :(',
                        'replies': [],
                    },
                ],
            },
            {
                'text': "Don't let reality ruin a good reddit clickbait.",
                'replies': [
                    {
                        'text': 'this app is being held together by the same couple dozen of reposts everyday',
                        'replies': [],
                    },
                ],
            },
        ],
    },
]


def create_comment_tree(author, video, nodes, parent=None):
    for node in nodes:
        comment = Comment.objects.create(
            user=author,
            text=node['text'],
            parent=parent,
        )
        VideoComment.objects.create(
            comment=comment,
            video=video,
        )
        if node.get('replies'):
            create_comment_tree(author, video, node['replies'], parent=comment)


@receiver(post_save, sender=Video)
def seed_fake_comments(sender, instance, created, **kwargs):
    if not created:
        return

    author = instance.user
    if not author:
        return

    create_comment_tree(author, instance, FAKE_COMMENTS)
