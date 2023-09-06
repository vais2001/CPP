def return_popup_value(condition):
    popup_value = ""
    if condition == "all_table":
        popup_value = 'openCaseDetailPage'
    if condition == "table_detail":
        popup_value = 'open_edit_popup'
    return popup_value

def return_unique_key(data_dict, table_name):
    if 'id' in data_dict.keys():
        value = "'"+str(data_dict['id'])+"'"+","+"'"+table_name+"'", 
    if 'table_name' in data_dict.keys():
        value = data_dict['table_name']
    print(data_dict,33333333333333333333333333333333333)
    return value


def generate_table_html(list_dict_data, condition, table_name):
        column_names = list(list_dict_data[0].keys())

        table_thead_html = """<thead>
                        <tr>"""
        for column in column_names:
            table_thead_html += f'<th scope="col">{column}</th>'
        table_thead_html += """
                            <th scope="col">Action</th>
                            </tr>
                            </thead>
                            """
        table_tbody_html = """<tbody>"""
        
        for data_dict in list_dict_data:
            table_tbody_html += '<tr>'
            for data in data_dict:
                table_tbody_html += f'<td>{data_dict[data]}</td>'
            
            popup_value = return_popup_value(condition)
            value = return_unique_key(data_dict, table_name)


            table_tbody_html += f"""<td>
                            <button class="border-0 bg-transparent me-2" data-placement="top" data-bs-toggle="modal" data-bs-target="#table_task_detail"
                            onclick={popup_value}{value}>
                                <i class="fa fa-edit"></i>
                            </button>
                            <h1>{popup_value}</h1>
                            <button class="border-0 bg-transparent" data-bs-placement="top" data-bs-toggle="modal"
                            onclick="add_delete_id_case('{value}')" data-bs-target="#deletion_table_data" title="Delete">
                                <i class="fa fa-trash"></i>
                            </button></td></tr>
                            """
        table_tbody_html += '</tbody>'

        return table_thead_html, table_tbody_html



class ListOfDotDicts(list):
    def __getitem__(self, index):
        item = super().__getitem__(index)
        if isinstance(item, dict):
            return DotDict(item)
        return item

class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr)

