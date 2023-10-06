from flask import request
from blueprint.notes import notes
from utils import respond_handle_wrapper, datetimeFormatString
from utils.dbpool import DatabaseConnectionPool

dbpool = DatabaseConnectionPool.getInstances()

query_field_tuple = ('md5', 'tags', 'timestamp', 'title', 'useful', 'author', 'id')
record_fields = ','.join(map(lambda x: f'`{x}`', query_field_tuple))


def parse_notes_record(records):
    for index, note in enumerate(records):
        note['id'] = index
        note['tags'] = note['tags'].split(',')
        note['timestamp'] = datetimeFormatString(note['timestamp'])
    return records[0] if len(records) == 1 else records


def pagination(req, sql_func):
    params = req.args.to_dict()
    num = int(params.get('num', '5'))
    page = int(params.get('page', '1'))
    sql = sql_func((page - 1) * num, num)
    result = dbpool.fetchall(sql)
    records = parse_notes_record(result)
    return records


def query_notes_later(start, num):
    return f"select {record_fields} from record order by `timestamp` desc limit {start}, {num}"


def query_notes_hottest(start, num):
    return f"select {record_fields} from record order by `useful` asc limit {start}, {num}"


def query_notes_tags():
    return 'select distinct tags from record;'


@notes.route('/tags', methods=['GET'])
@respond_handle_wrapper
def query_tags():
    md5 = request.args.get('md5', None)
    sql = f"select {record_fields} from record where md5={md5}"
    res = dbpool.fetchone(sql)
    return res


@notes.route('/tags/count', methods=['GET'])
@respond_handle_wrapper
def query_count_tags():
    tag_dict = {}
    tags = dbpool.fetchall(query_notes_tags())
    tag_list = ','.join(map(lambda items: items['tags'], tags)).split(',')
    for tag in tag_list:
        tag_dict.setdefault(tag, 0)
        tag_dict[tag] += 1
    return tag_dict


@notes.route('/record', methods=['GET'])
@respond_handle_wrapper
def query_notes_record():
    sql = 'select id, title, md5, tags, `timestamp`, useful  from record where status=1;'
    record_list = dbpool.fetchall(sql)
    records = parse_notes_record(record_list)
    return records


@notes.route('/record/later', methods=['GET'])
@respond_handle_wrapper
def query_note_later():
    query_notes_list = pagination(request, query_notes_later)
    return query_notes_list


@notes.route('/record/hottest', methods=['GET'])
def query_note_hottest():
    query_note_list = pagination(request, query_notes_hottest)
    return query_note_list


@notes.route('/record/filter', methods=['GET'])
@respond_handle_wrapper
def query_record_filter_field():
    query_note_list = []
    field = request.args.get('field', None)
    value = request.args.get('value', None)
    if field is None or value is None:
        return query_note_list

    if field in ("tags", "md5"):
        cond = ' or '.join(map(lambda v: f"{field} like '%{v}%'", value.split(',')))
        sql = f"select {record_fields} from record WHERE {cond};"
        fetch_result = dbpool.fetchall(sql)
        query_note_list = parse_notes_record(fetch_result)

    return query_note_list


@notes.route('/details', methods=['GET'])
@respond_handle_wrapper
def query_note_details():
    params = request.args.to_dict()
    md5 = params.get('md5', '')
    library_sql = f"select content from library where md5='{md5}';"
    library = dbpool.fetchone(library_sql)
    return library or {"content": None}
