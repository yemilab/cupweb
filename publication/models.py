from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from home.custom_fields import TranslatedField


DATEFMT = [
    ('Y', 'Year'),
    ('YM', 'Year-Month'),
    ('YMD', 'Year-Month-Date'),
]

DEGREE = [
    ('PhD', 'Ph.D.'),
    ('MS', 'Master')
]

PAPERTYPE = [
    ('CP', 'Conference proceeding'),
    ('JA', 'Journal article')
]

NOTEGROUP = [
    ('GENERAL', 'GENERAL'),
    ('KIMS', 'KIMS'),
    ('AMORE', 'AMORE'),
    ('SBL', 'SBL'),
    ('SIMULATION', 'SIMULATION'),
]

NOTECLASSIFICATION = [
    ('PHYS', 'PHYS'),
    ('ANAL', 'ANAL'),
    ('HARD', 'HARD'),
    ('SOFT', 'SOFT'),
    ('THESIS', 'THESIS'),
    ('PUB', 'PUB'),
    ('DOC', 'DOC'),
]


@register_snippet
class Journal(models.Model):
    title = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Journals"


class PresentationPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PresentationPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PresentationPage(Page):
    is_featured = models.BooleanField()
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    date = models.DateField("Presentation date")
    date_fmt = models.CharField("Date format", max_length=8, choices=DATEFMT, default='YMD')
    abstract = RichTextField(blank=True, null=True)
    extra = RichTextField(blank=True, null=True)
    tags = ClusterTaggableManager(through=PresentationPageTag, blank=True)
    presentor = models.ForeignKey(
        'home.Person',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
    )
    meeting = models.CharField(max_length=512)
    country = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('is_featured'),
        ImageChooserPanel('cover_image'),
        SnippetChooserPanel('presentor'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('meeting', classname="col10"),
            ]),
            FieldRowPanel([
                FieldPanel('country', classname="col6"),
                FieldPanel('location', classname="col6"),
            ]),
        ], "Meeting information"),
        FieldPanel('date_fmt'),
        FieldPanel('date'),
        FieldPanel('tags'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('extra', classname="full"),
    ]

    subpage_types = [ ]
    parent_page_types = ['PresentationsIndexPage', ]


class PresentationsIndexPage(Page):
    title_ko = models.CharField("Title (Korean)", max_length=255)
    tr_title = TranslatedField(
        'title',
        'title_ko',
    )
    description = models.TextField(
        "Description (English)",
        help_text='Text to describe the page',
        blank=True)
    description_ko = models.TextField(
        "Description (Korean)",
        help_text='Text to describe the page',
        blank=True)
    tr_description = TranslatedField(
        'description',
        'description_ko',
    )

    content_panels = Page.content_panels + [
        FieldPanel('title_ko'),
        FieldPanel('description', classname="full"),
        FieldPanel('description_ko', classname="full"),
    ]

    subpage_types = ['PresentationPage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_presentations(self):
        return PresentationPage.objects.live().descendant_of(self).order_by('-date')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_presentations(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(PresentationsIndexPage, self).get_context(request)
        presentations = self.paginate(request, self.get_presentations())
        context['presentations'] = presentations
        return context


class PaperPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PaperPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PaperPage(Page):
    is_featured = models.BooleanField()
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    date = models.DateField("Published date")
    date_fmt = models.CharField("Date format", max_length=8, choices=DATEFMT, default='YMD')
    abstract = RichTextField(blank=True, null=True)
    extra = RichTextField(blank=True, null=True)
    tags = ClusterTaggableManager(through=PaperPageTag, blank=True)
    authors = models.TextField()
    journal = models.ForeignKey(
        'publication.Journal',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    volume = models.CharField(max_length=64, blank=True, null=True)
    issue = models.CharField(max_length=64, blank=True, null=True)
    page = models.CharField(max_length=64, blank=True, null=True)
    doi = models.CharField(max_length=250, blank=True, null=True)
    permalink = models.URLField("Permanent link", blank=True, null=True)
    bibtex = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('is_featured'),
        ImageChooserPanel('cover_image'),
        FieldPanel('authors'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('journal'),
            ]),
            FieldRowPanel([
                FieldPanel('volume'),
                FieldPanel('issue'),
                FieldPanel('page'),
            ]),
        ], "Reference information"),
        FieldPanel('date_fmt'),
        FieldPanel('date'),
        FieldPanel('tags'),
        FieldPanel('doi'),
        FieldPanel('permalink'),
        FieldPanel('bibtex'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('extra', classname="full"),
    ]

    subpage_types = [ ]
    parent_page_types = ['PapersIndexPage', ]


class PapersIndexPage(Page):
    title_ko = models.CharField("Title (Korean)", max_length=255)
    tr_title = TranslatedField(
        'title',
        'title_ko',
    )
    description = models.TextField(
        "Description (English)",
        help_text='Text to describe the page',
        blank=True)
    description_ko = models.TextField(
        "Description (Korean)",
        help_text='Text to describe the page',
        blank=True)
    tr_description = TranslatedField(
        'description',
        'description_ko',
    )

    content_panels = Page.content_panels + [
        FieldPanel('title_ko'),
        FieldPanel('description', classname="full"),
        FieldPanel('description_ko', classname="full"),
    ]

    subpage_types = ['PaperPage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_papers(self):
        return PaperPage.objects.live().descendant_of(self).order_by('-date')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_papers(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(PapersIndexPage, self).get_context(request)
        papers = self.paginate(request, self.get_papers())
        context['papers'] = papers
        return context


class ThesisPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ThesisPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ThesisPage(Page):
    date = models.DateField("Published date")
    date_fmt = models.CharField(max_length=8, choices=DATEFMT, default='YMD')
    abstract = RichTextField(blank=True, null=True)
    extra = RichTextField(blank=True, null=True)
    tags = ClusterTaggableManager(through=ThesisPageTag, blank=True)
    author = models.ForeignKey(
        'home.Person', related_name='+', on_delete=models.PROTECT
    )
    degree = models.CharField("Academic degree", max_length=8, choices=DEGREE, default='PhD')
    publisher = models.CharField(max_length=250)
    advisor = models.CharField(max_length=250, blank=True)

    content_panels = Page.content_panels + [
        SnippetChooserPanel('author'),
        FieldPanel('degree'),
        FieldPanel('publisher'),
        FieldPanel('date_fmt'),
        FieldPanel('date'),
        FieldPanel('advisor'),
        FieldPanel('abstract', classname="full"),
        FieldPanel('tags'),
        FieldPanel('extra', classname="full"),
    ]

    subpage_types = [ ]
    parent_page_types = ['ThesesIndexPage', ]


class ThesesIndexPage(Page):
    title_ko = models.CharField("Title (Korean)", max_length=255)
    tr_title = TranslatedField(
        'title',
        'title_ko',
    )
    description = models.TextField(
        "Description (English)",
        help_text='Text to describe the page',
        blank=True)
    description_ko = models.TextField(
        "Description (Korean)",
        help_text='Text to describe the page',
        blank=True)
    tr_description = TranslatedField(
        'description',
        'description_ko',
    )

    content_panels = Page.content_panels + [
        FieldPanel('title_ko'),
        FieldPanel('description', classname="full"),
        FieldPanel('description_ko', classname="full"),
    ]

    subpage_types = ['ThesisPage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_theses(self):
        return ThesisPage.objects.live().descendant_of(self).order_by('-date')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_theses(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(ThesesIndexPage, self).get_context(request)
        theses = self.paginate(request, self.get_theses())
        context['theses'] = theses
        return context


class NotePersonRelationship(Orderable, models.Model):
    note = ParentalKey(
        'NotePage', related_name='note_document_relationship', on_delete=models.CASCADE
    )
    document = models.ForeignKey(
        'wagtaildocs.Document', related_name='document_note_relationship', on_delete=models.CASCADE
    )
    panels = [
        DocumentChooserPanel('document')
    ]


class NotePageTag(TaggedItemBase):
    content_object = ParentalKey(
        'NotePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class NotePage(Page):
    date = models.DateField("Published date")
    tags = ClusterTaggableManager(through=NotePageTag, blank=True)
    group = models.CharField(max_length=64, choices=NOTEGROUP)
    classification = models.CharField(max_length=64, choices=NOTECLASSIFICATION)
    number = models.IntegerField(unique=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('group'),
        FieldPanel('classification'),
        FieldPanel('number'),
        InlinePanel(
            'note_document_relationship', label="Document(s)",
            panels=None, min_num=1),
        FieldPanel('tags'),
    ]

    subpage_types = [ ]
    parent_page_types = ['NotesIndexPage', ]


class NotesIndexPage(Page):
    title_ko = models.CharField("Title (Korean)", max_length=255)
    tr_title = TranslatedField(
        'title',
        'title_ko',
    )
    description = models.TextField(
        "Description (English)",
        help_text='Text to describe the page',
        blank=True)
    description_ko = models.TextField(
        "Description (Korean)",
        help_text='Text to describe the page',
        blank=True)
    tr_description = TranslatedField(
        'description',
        'description_ko',
    )

    content_panels = Page.content_panels + [
        FieldPanel('title_ko'),
        FieldPanel('description', classname="full"),
        FieldPanel('description_ko', classname="full"),
    ]

    subpage_types = ['NotePage', ]
    parent_page_types = ['home.SectionPage', ]

    def get_notes(self):
        return NotePage.objects.live().descendant_of(self).order_by('-date')

    def children(self):
        return self.get_children().specific().live()

    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_notes(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_context(self, request):
        context = super(NotesIndexPage, self).get_context(request)
        notes = self.paginate(request, self.get_notes())
        context['notes'] = notes
        return context
