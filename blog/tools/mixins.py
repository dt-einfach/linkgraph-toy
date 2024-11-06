from .. import permissions


class IsWriterMixin:
    permission_classes = [permissions.IsWriter]


class IsEditorMixin:
    permission_classes = [permissions.IsEditor]
