def get_document(self):
    tags_ids = self.taga_ids.ids
    doc_table_ids = self.order_line.mapped("product_template_id.documents_ids")
    doc_ids = [rec.id for rec in doc_table_ids for rc in rec.tags_id if
               rc.id in tags_ids]
    self.documents_ids = [(6, 0, doc_ids)]


def get_documents(self):
    """create record in documents page"""
    doc_ids = []
    tag_ids = self.tags_ids.ids
    product_doc_ids = self.order_line.mapped(
        'product_template_id.documents_ids')
    for rec in product_doc_ids:
        for rt in rec.tag_ids:
            if rt.id in tag_ids and rec.id not in doc_ids:
                doc_ids.append(rec.id)
    self.documents_ids = [(6, 0, doc_ids)]


def get_documents(self):
    """create record in documents page"""
    tag_ids = set(self.tags_ids.ids)  # set for faster membership checks
    product_doc_ids = self.order_line.mapped(
        'product_template_id.documents_ids')
    doc_ids = list(filter(lambda rec: any(i.id in tag_ids for i in tag_ids),
                          product_doc_ids))
