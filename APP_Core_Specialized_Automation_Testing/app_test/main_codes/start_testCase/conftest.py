# -*- coding:utf-8 -*-

# @Author       : baolong.wang
# @Date         : 2024/2/7 14:52
# @File         : conftest.py
# @Mark         :
# @TechnicalBarriers:
# @KnowledgePoints:


import pytest
import time
import os
import io
import logging
from datetime import datetime
from py.xml import html

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)

'''修改报告标题'''
@pytest.mark.optionalhook
def pytest_html_report_title(report):
    titleName = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
    report.title = f"Automation_Test_Report_{titleName}"


def pytest_html_results_table_header(cells):
    '''修改表头属性：增加Time列，删除Link列'''
    cells.insert(2, html.th('Status', class_='sortable col-status'))
    cells.insert(0, html.th('Time', class_='sortable time', col='time'))
    cells.pop(1)
    cells.insert(2, html.th('Test Case Alias', class_='sortable col-test'))
    cells.pop(-1)  # 删除最后一列


def pytest_html_results_table_row(report, cells):
    '''修改表格属性，同步表头修改'''
    cells.insert(0, html.td(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), class_='col-time'))
    cells.pop(1)

    test_function_name = report.nodeid.split('::')[-1].split('[')[0].strip()

    test_function_aliases = {
        'test_app_login': 'APP 账号密码登录',
        'test_AF103_buleboothBindDevice': 'AF103 蓝牙绑定设备',
        'test_AF103_addAndApplyFeedCall': 'AF103 添加与应用喂食录音',
        'test_AF103_manualFeed': 'AF103 手动喂食',
        'test_AF103_scheduleFeed': 'AF103 计划喂食',
        'test_AF103_ota': 'AF103 OTA',
        'test_AF103_unbindDevice': 'AF103 解绑设备',
    }

    test_function_alias = test_function_aliases.get(test_function_name, '')
    cells.insert(2, html.td(test_function_alias, class_='col-test'))
    cells.pop(-1)

    if report.passed:
        cells.insert(3, html.td('PASSED', class_='col-pass', color_='green', style='text-align:left; color: green; font-weight: bold;'))
    elif report.failed:
        cells.insert(3, html.td('FAILED', class_='col-fail', style='text-align:left; color: red; font-weight: bold;'))
    elif report.skipped:
        cells.insert(3, html.td('SKIPPED', class_='col-skip', style='text-align:left; color: gray; font-weight: bold;'))
    else:
        cells.insert(3, html.td('UNKNOWN STATUS', class_='col-unknown', style='text-align:left; color: orange; font-weight: bold;'))


@pytest.fixture(scope='function', autouse=True)
def log_test(request):
    # 创建一个内存中的日志处理器
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # 获取当前测试用例的根 logger
    logger = logging.getLogger()
    logger.addHandler(handler)

    # 在测试用例执行后移除日志处理器
    def remove_handler():
        logger.removeHandler(handler)
    request.addfinalizer(remove_handler)

# @pytest.fixture(scope='function', autouse=True)
# def log_test(request):
#     # Create an in-memory log handler
#     log_capture = io.StringIO()
#     handler = logging.StreamHandler(log_capture)
#     formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#
#     # Get the root logger of the current test case
#     logger = logging.getLogger()
#     logger.addHandler(handler)
#
#     # After executing the test case, remove the log handler
#     def remove_handler():
#         if log_capture.getvalue():
#             # Save the log content to the extra field of the report
#             log_contents = log_capture.getvalue()
#             setattr(request.node, 'log', log_contents)
#         logger.removeHandler(handler)
#
#     request.addfinalizer(remove_handler)

# @pytest.mark.optionalhook
# def pytest_html_results_table_html(report, data):
#     if hasattr(report, 'log'):
#         from html import escape  # This is where escape should be imported from
#         extra_log = escape(report.log)  # Utilize the escape function from the standard library
#         # data.append(html.div(html.pre(extra_log), class_='log'))
#         data.append(html.div(html.pre(extra_log.encode('utf-8').decode('utf-8')), class_='log'))

# @pytest.mark.optionalhook
# def pytest_html_results_table_html(report, data):
#     if hasattr(report, 'log'):
#         log_bytes = report.log.encode()
#         result = chardet.detect(log_bytes)
#         log_encoding = result['encoding']
#         if log_encoding != 'utf-8':
#             log_bytes = log_bytes.decode(log_encoding).encode('utf-8')
#         extra_log = log_bytes.decode('utf-8')
#         data.append(html.div(html.pre(extra_log), class_='log'))

@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if hasattr(report, 'log'):
        log_utf8 = report.log.encode('utf-8').decode('utf-8')
        data.append(html.div(html.pre(log_utf8), class_='log'))

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if item.function.__doc__ is None:
        report.description = str(item.function.__name__)        # 如果没有三引号注释（'''注释'''），就提取函数名到case的输出文案中，就是上面的test_id
    else:
        report.description = str(item.function.__doc__)            # 提取三引号注释（'''注释'''）到case的输出文案中
    report.nodeid = report.nodeid.encode("unicode_escape").decode("utf-8")  # 再把编码改回来


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    current_script_path = os.path.abspath(__file__)  # 获取当前脚本文件的绝对路径
    script_dir = os.path.dirname(current_script_path)  # 获取脚本所在的目录
    os.chdir(script_dir)  # 切换工作目录至脚本所在目录

    reportName = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    config.option.htmlpath = f"../report/Automation_Test_Report_{reportName}.html"
