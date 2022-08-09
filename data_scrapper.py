import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json


def get_raw_courses(ineuron_url):
    resp = requests.get(ineuron_url)
    ineuron_html = bs(resp.text, "html.parser")
    course_boxes = ineuron_html.findAll("script", {"id": "__NEXT_DATA__"})
    main_data = course_boxes[0].contents[0]
    main_data_dict = json.loads(main_data)
    init_course_data = main_data_dict["props"]["pageProps"]["initialState"]["init"]
    return init_course_data


def structured_course_data(raw_data):
    subCat_to_Cat = raw_data["categories"]
    course_to_instructor = raw_data["instructors"]
    course_data = raw_data["courses"]
    final_data = dict()
    for k in course_data:
        final_data[k] = {}
        final_data[k]["Description"] = course_data[k]["description"]
        try:
            try:
                if course_data[k]["pricing"]["isFree"] == False:
                    final_data[k]["Price"] = course_data[k]["pricing"]["IN"]
                else:
                    final_data[k]["Price"] = "Free"
            except:
                final_data[k]["Price"] = course_data[k]["batches"][0]["pricing"]["IN"]
        except:
            final_data[k]["Price"] = "Free"

        for c in subCat_to_Cat:
            for sc in subCat_to_Cat[c]["subCategories"]:
                if sc == course_data[k]["categoryId"]:
                    final_data[k]["Category"] = subCat_to_Cat[c]["title"]
                    final_data[k]["SubCategory"] = subCat_to_Cat[c]["subCategories"][
                        sc
                    ]["title"]

        final_data[k]["Instructor(s)"] = dict()

        if course_data[k]["courseMeta"][0]["instructors"] != list():
            for ins in course_data[k]["courseMeta"][0]["instructors"]:
                for ins_id in course_to_instructor:
                    if ins == ins_id:
                        final_data[k]["Instructor(s)"][
                            course_to_instructor[ins_id]["name"]
                        ] = dict()
                        try:
                            final_data[k]["Instructor(s)"][
                                course_to_instructor[ins_id]["name"]
                            ]["email"] = course_to_instructor[ins_id]["email"]
                        except:
                            final_data[k]["Instructor(s)"][
                                course_to_instructor[ins_id]["name"]
                            ]["email"] = "NA"
                        try:
                            final_data[k]["Instructor(s)"][
                                course_to_instructor[ins_id]["name"]
                            ]["Description"] = course_to_instructor[ins_id][
                                "description"
                            ]
                        except:
                            final_data[k]["Instructor(s)"][
                                course_to_instructor[ins_id]["name"]
                            ]["Description"] = "NA"
        else:
            final_data[k]["Instructor(s)"] = "None"
    final_data_list=[]
    for i in final_data:
        buff_dict={i:final_data[i]}
        final_data_list.append(buff_dict)
    return final_data_list

