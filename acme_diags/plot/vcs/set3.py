import os
import copy
import vcs
import cdms2
from genutil import udunits
from acme_diags.driver.utils import get_output_dir

vcs_canvas = vcs.init()

def set_units(ref_or_test, units):
    if units != '':
        ref_or_test.units = units

def plot(ref, test, diff, metrics_dict, parameters):
    # Line options, see here: https://uvcdat.llnl.gov/documentation/vcs/vcs-10.html
    # Other options not in the above link: https://uvcdat.llnl.gov/docs/vcs/graphics/unified1D.html
    ref_plot_linetype = 0
    ref_plot_color = 1  # 6 to 239
    ref_plot_width = 3  # 1 to 100
    ref_plot_marker = 1
    ref_plot_markersize = 1
    ref_plot_markercolor = 1

    test_plot_linetype = 0
    test_plot_color = 215
    test_plot_width = 3
    test_plot_marker = 1
    test_plot_markersize = 1
    test_plot_markercolor = 215

    diff_plot_linetype = 0
    diff_plot_color = 1
    diff_plot_width = 3
    diff_plot_marker = 1
    diff_plot_markersize = 1
    diff_plot_markercolor = 1


    vcs_canvas.geometry(parameters.canvas_size_w, parameters.canvas_size_h)
    vcs_canvas.drawlogooff()

    set_units(test, parameters.test_units)
    set_units(ref, parameters.reference_units)
    set_units(diff, parameters.diff_units)

    test.long_name = parameters.test_title
    ref.long_name = parameters.reference_title
    diff.long_name = parameters.diff_title

    #test.id = parameters.test_name
    #ref.id = parameters.reference_name
    #diff.id = parameters.diff_name

    # use vcs_canvas.show('colormap') to view all colormaps
    vcs_canvas.setcolormap('rainbow')  # 6 to 239 are purple to red in rainbow order

    ref_test_template = vcs.createtemplate('ref_test_template')
    # make all of the elements listed have priority = 0
    ref_test_template.blank(["mean", "max", "min", "zvalue", "dataname", "crtime", "ytic2", "xtic2"])

    # the actual box around the plot
    ref_test_template.box1.x1 = 0.123
    ref_test_template.box1.x2 = 0.86
    ref_test_template.box1.y1 = 0.55
    ref_test_template.box1.y2 = 0.90

    # data (the lines) need to be offset accordingly
    ref_test_template.data.x1 = 0.123
    ref_test_template.data.x2 = 0.86
    ref_test_template.data.y1 = 0.55
    ref_test_template.data.y2 = 0.90

    ref_test_template.legend.x1 = 0.88
    ref_test_template.legend.x2 = 0.98
    ref_test_template.legend.y1 = 0.86
    ref_test_template.legend.y2 = 0.88
    ref_test_template.legend.textorientation = 'defright'

    ref_test_template.title.x = 0.5
    ref_test_template.title.textorientation = 'defcenter'

    ref_test_template.units.x = 0.85
    ref_test_template.units.y = 0.91

    # labels on xaxis
    ref_test_template.xlabel1.y = (0.55) - 0.02  # no xlabel1.x attribute

    # actual ticks on xaxis
    ref_test_template.xtic1.y1 = (0.55 - 0.005) + 0.01
    ref_test_template.xtic1.y2 = (0.55 - 0.005)

    # name of xaxis
    ref_test_template.xname.y += 0.29

    # labels on yaxis
    ref_test_template.ylabel1.x = 0.1108  # no ylabel1.y attribute

    # actual ticks on yaxis
    ref_test_template. ytic1.x1 = (0.123 - 0.005) + 0.01
    ref_test_template.ytic1.x2 = (0.123 - 0.005)

    # name of yaxis
    ref_test_template.yname.x += 0.05
    ref_test_template.yname.y += 0.17


    diff_template = vcs.createtemplate('diff_template', ref_test_template)
    diff_template.box1.y1 -= 0.47
    diff_template.box1.y2 -= 0.47

    diff_template.data.y1 -= 0.47
    diff_template.data.y2 -= 0.47

    diff_template.legend.y1 -= 0.47
    diff_template.legend.y2 -= 0.47

    diff_template.title.y -= 0.47
    diff_template.units.y -= 0.47

    diff_template.xlabel1.y -= 0.47

    diff_template.xtic1.y1 -= 0.47
    diff_template.xtic1.y2 -= 0.47

    diff_template.xname.y -= 0.47
    diff_template.yname.y -= 0.47



    ref_line = vcs_canvas.createxvsy('ref_plot')
    ref_line.datawc_y1 = min(ref.min(), test.min())
    ref_line.datawc_y2 = max(ref.max(), test.max())

    test_line = vcs_canvas.createxvsy('test_plot')
    test_line.datawc_y1 = min(ref.min(), test.min())
    test_line.datawc_y2 = max(ref.max(), test.max())

    diff_line = vcs_canvas.createxvsy('diff_plot')
    diff_line.datawc_y1 = diff.min()
    diff_line.datawc_y2 = diff.max()


    #ref_line.line = ref_plot_linetype
    ref_line.linetype = ref_plot_linetype
    ref_line.linecolor = ref_plot_color
    ref_line.linewidth = ref_plot_width
    ref_line.marker = ref_plot_marker
    ref_line.markersize = ref_plot_markersize
    ref_line.markercolor = ref_plot_markercolor

    #test_line.line = test_plot_linetype
    test_line.linetype = test_plot_linetype
    test_line.linecolor = test_plot_color
    test_line.linewidth = test_plot_width
    test_line.marker = test_plot_marker
    test_line.markersize = test_plot_markersize
    test_line.markercolor = test_plot_markercolor
    # test_line.smooth = 1

    #diff_line.line = diff_plot_linetype
    diff_line.linetype = diff_plot_linetype
    diff_line.linecolor = diff_plot_color
    diff_line.linewidth = diff_plot_width
    diff_line.marker = diff_plot_marker
    diff_line.markersize = diff_plot_markersize
    diff_line.markercolor = diff_plot_markercolor

    blank_template = vcs_canvas.createtemplate('blank_template', ref_test_template)
    blank_template.blank()
    blank_template.legend.priority = 1
    blank_template.legend.y1 -= 0.05
    blank_template.legend.y2 -= 0.05

    vcs_canvas.plot(ref, ref_line, ref_test_template)
    vcs_canvas.plot(test, test_line, blank_template)
    vcs_canvas.plot(diff, diff_line, diff_template)

    # Plot the main title
    # TODO make this use managetextcombined() later
    main_title = vcs.createtextcombined('main_title')
    main_title.string = 'Main Title'
    main_title.height = 18
    main_title.halign = 'center'
    main_title.x = 0.5
    main_title.y = 0.97
    vcs_canvas.plot(main_title)

    ref_test_template.script('plot_set_3.json')
    blank_template.script('plot_set_3.json')
    diff_template.script('plot_set_3.json')
    ref_line.script('plot_set_3.json')
    test_line.script('plot_set_3.json')
    diff_line.script('plot_set_3.json')
    main_title.script('plot_set_3.json')

    fnm = os.path.join(get_output_dir('3', parameters), parameters.output_file)
    for f in parameters.output_format:
        f = f.lower().split('.')[-1]
        if f == 'png':
            vcs_canvas.png(fnm)
        elif f == 'pdf':
            vcs_canvas.pdf(fnm)
        elif f == 'svg':
            vcs_canvas.svg(fnm)

        print('Plot saved in: ' + fnm + '.' + f)
    vcs_canvas.clear()
