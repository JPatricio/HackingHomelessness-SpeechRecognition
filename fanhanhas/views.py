import gensim

from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from fanhanhas.models import Report
from fanhanhas.nlp_utils import transcript_preprocessing


def index(request):
    """
    Session recording page. No fancy logic here, just return template
    :param request:
    :return:
    """
    return render(request, 'fanhanhas/index.html', dict())


def report_list(request):
    """
    View for list of all reports
    :param request:
    :return:
    """
    user_sessions = dict()
    clients = set()

    # Get all distinct clients.
    # TODO: In production, change to objects.distinct. It is not supported by sqllite
    for r in Report.objects.all():
        clients.add(r.client)
    clients = list(clients)
    clients.sort()

    # Get past session for each found client
    for user in clients:
        user_sessions[user] = Report.objects.filter(client=user)

    return render(request, 'fanhanhas/report_list.html', dict(reports=user_sessions))


def report(request):
    """
    View for visualizing the report
    :param request:
    :return:
    """
    # Fetch report from db
    id = request.GET['id']
    report = Report.objects.get(id=id)

    # Do some pre-processing for highlighting the found topics in the transcript
    transcript = report.transcript
    topics = report.topics.split(";")
    for topic in topics:
        if topic != "":
            transcript = transcript.replace(topic, "<mark>%s</mark>" % topic)

    return render(request,
                  'fanhanhas/report.html',
                  dict(
                      report=report,
                      topic1=topics[0],
                      topic2=topics[1],
                      topic3=topics[2],
                      topic4=topics[3],
                      transcript=transcript
                  )
    )


@csrf_exempt
def report_generator(request):
    """
    This view will get the transcript, generate topics, and save the whole thing to the database
    :param request:
    :return:
    """
    # Extract request data
    client = request.POST.get("client", "")
    text = request.POST.get("text", "")

    # Prepare transcript to be consumable by gensim model.
    tokens = [transcript_preprocessing(text)]

    # Create our word dictionary and corpus
    dictionary = gensim.corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(text) for text in tokens]

    # No real need to persist out stuff but good to know how it goes
    # pickle.dump(corpus, open('corpus.pkl', 'wb'))
    # dictionary.save('dictionary.gensim')

    # Is 4 models a good assumption for this? Typically conversations will range anywhere from 15 to 60 minutes
    NUM_TOPICS = 4
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)

    # Lastly we will take the highest scoring word of each topic
    # TODO: Obviously should save all words of all topics, and their ranks. This is very rich information.
    # TODO: But for the sake of this Hackaton, it's all good in the hood.

    topics = list()
    for topicnum in range(NUM_TOPICS):
        highest_pow = -10
        best_word = ""
        for (word, pow) in ldamodel.show_topic(topicnum, NUM_TOPICS):
            if pow > highest_pow and word not in topics:
                highest_pow = pow
                best_word = word
        print(topicnum)
        topics.append(best_word)


    Report.objects.get_or_create(client=client,
                                 transcript=text,
                                 topics="%s;%s;%s;%s" % (topics[0],
                                                         topics[1],
                                                         topics[2],
                                                         topics[3]
                                                         )
                                 )

    return JsonResponse(dict(topic1=topics[0],
                             topic2=topics[1],
                             topic3=topics[2],
                             topic4=topics[3]
                             )
                        )
