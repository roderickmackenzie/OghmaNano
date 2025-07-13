%This is a script to run OghmaNano through MATLAB
%Mainly written by Dr Jun Yan: yanjunever@gmail.com 09/02/2022
%Modified by Roderick MacKenzie 09/02/2022

%To use this script you will have to:
%Add the install path of OghmaNano to your system paths
%https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ee537574(v=office.14)
%***You will then have to restart matlab for the change to take effect.***

%%
clc 
clear all
close all
set(0, 'DefaultLineLineWidth', 0.5);

%% choose the folder where you do the simulations (the folder must contain a *.oghma file)
origional_path = uigetdir('C:\','select a folder to run simulations');
%% %%defalut%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%If we are on linux oghma_core does not end with .exe
exe_ext=".exe";
if isunix==true
    exe_ext="";
end

if exist("sim.oghma", 'file')==false
 sprintf("No sim.oghma file found");
end

%The sim.oghma file is a zip file with sim.json inside
%sim.json is a text file in json format. We need to 
%extract sim.json from the zip file before we can edit in matlab.

if exist("sim.json", 'file')==false
 unzip("sim.oghma")
end
%read json file
A = fileread("sim.json");
json_data=jsondecode(A);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% start of OghmaNano simulations
%set simulation mode
json_data.sim.simmode='segment0@jv';							%jv scan
%set name for scan folder
base_dir="bdir_scan";

%Clean up/delete the folder with the same simulation name
%Taken out due to paranoia, the matlab rmdir command does not work on windows
%You will have to go and find cmd_rmdir to make this line work
%cmd_rmdir(fullfile(origional_path,base_dir))

%set variable range
variable=logspace(-20,-6,15);
%start of loop for multiples simulations
for bdir=variable
    %make directory for each simulation condition and change to the
    %corresponding path
    dir_name=sprintf("%e",bdir);
    full_path=fullfile(origional_path,base_dir,dir_name);
    mkdir(full_path)
    cd(full_path)
    %change variables of interest
    json_data.epitaxy.segment2.shape_dos.free_to_free_recombination=bdir;       %Change variable of layer2
    %copy simulation file to each sub-folder in order to run separately
    copyfile(fullfile(origional_path,"sim.oghma"),fullfile(origional_path,base_dir,dir_name,"sim.oghma"))
    %read json files
    out=jsonencode(json_data);
    json_data;
    %show instant simulation progress
    fid = fopen("sim.json",'w');
    fprintf(fid, '%s', out);
    fclose(fid);
    %run OghmaNano simulations
    system("oghma_core"+exe_ext)
    
end
%change back to the origonal path, i.e. the one you want to run the
%simulations
cd(origional_path)
% end of OghmaNano simualations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% plots
%% plot JVs
cd(origional_path)
base_dir="bdir_scan";
variable=logspace(-20,-6,15);
for bdir=variable
    dir_name=sprintf("%e",bdir);
    full_path=fullfile(origional_path,base_dir,dir_name);
    cd(full_path)
    files_to_plot = importdata("jv.csv");
    figure (1)
    plot(files_to_plot.data(:,1),files_to_plot.data(:,2)/10,'DisplayName',num2str(bdir))
    axis([0 1.2 -30 0])
    hold on
end
cd(origional_path)
%rmdir(base_dir,'s')
    title(base_dir)
    xlabel('Voltage (V)','fontsize',14)
    ylabel('Current density (mA cm^{-2})','fontsize',14)
    set(gcf,'color','w');
    legend show
    
    saveas(figure(1),['JV-',base_dir{1},'.fig']);

%% plot sim_info.dat
cd(origional_path)
for bdir=variable
    dir_name=sprintf("%e",bdir);
    full_path=fullfile(origional_path,base_dir,dir_name);
    cd(full_path)
    AA = fileread("sim_info.dat");
    json_data_sim_info=jsondecode(AA);
    
    %FF
        figure (2)
        subplot(2,2,1)
    semilogx(bdir,str2num(json_data_sim_info.ff),'*','markersize',10) %#ok<ST2NM>
    hold on
        %title(base_dir)
    xlabel('Bdir (m^3 s^{-1})','fontsize',14)
    ylabel('FF','fontsize',14)
    set(gcf,'color','w');
    %Jsc
            figure (2)
        subplot(2,2,2)
    semilogx(bdir,abs(str2num(json_data_sim_info.jsc)),'*','markersize',10) %#ok<ST2NM>
    hold on
        %title(base_dir)
    xlabel('Bdir (m^3 s^{-1})','fontsize',14)
    ylabel('Jsc','fontsize',14)
    set(gcf,'color','w');
        %Voc
            figure (2)
        subplot(2,2,3)
    semilogx(bdir,abs(str2num(json_data_sim_info.voc)),'*','markersize',10) %#ok<ST2NM>
    hold on
       % title(base_dir)
    xlabel('Bdir (m^3 s^{-1})','fontsize',14)
    ylabel('Voc','fontsize',14)
    set(gcf,'color','w');
    
   %pce
            figure (2)
        subplot(2,2,4)
    semilogx(bdir,abs(str2num(json_data_sim_info.pce)),'*','markersize',10) %#ok<ST2NM>
    hold on
        %title(base_dir)
    xlabel('Bdir (m^3 s^{-1})','fontsize',14)
    ylabel('PCE','fontsize',14)
    set(gcf,'color','w');
end
%rmdir(base_dir,'s')

cd(origional_path)
    
saveas(figure(2),['sim-info-',base_dir{1},'.fig']);
