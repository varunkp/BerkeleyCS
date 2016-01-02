function [eig_faces, D, dimensions] = eigenfaces()

counter = 1;
cel_dir = dir('CelebrityDatabase/*.jpg');
stud_dir = dir('StudentDatabase/*.jpg');
celebs_raw = cell(1, length(cel_dir));
students_raw = cell(1,length(stud_dir));

celeb_X = [];
student_X = [];


mask = load('mask.mat');
mask = mask.mask;

unmasked_pixels = find(mask(:,:,1));
masked_pixels = find(~mask);

for i = 1: length(cel_dir)
    celebs_raw{i} = rgb2gray(imread(['CelebrityDatabase/' cel_dir(i).name]));
    im_vector = celebs_raw{i}(unmasked_pixels);
    celebs_raw{i} = im_vector;
    celeb_X = [celeb_X, celebs_raw{i}];
    %celeb_X = [celeb_X, reshape(celebs_raw{i}, [size(celebs_raw{i},1) * size(celebs_raw{i},2), 1])];
end
for i = 1:length(stud_dir)
    students_raw{i} = rgb2gray(imread(['StudentDatabase/' stud_dir(i).name]));
    im_vector = students_raw{i}(unmasked_pixels);
    students_raw{i} = im_vector;
    student_X = [student_X, students_raw{i}];
    %student_X = [student_X, reshape(students_raw{i}, [size(students_raw{i},1) * size(students_raw{i},2), 1])];
end

celeb_X = double(celeb_X);
student_X = double(student_X);

a = mean(celeb_X,2);
std_dev = std(celeb_X);

figure(counter);
counter = counter + 1;
temp_mean = zeros(330,280);
temp_mean(unmasked_pixels) = a;
%raw_image_mean = reshape(a, size(celebs_raw{1}));

raw_image_mean = mat2gray(temp_mean);
imshow(raw_image_mean);

%size(celeb_X, 2)

u = a(:,ones(1, size(celeb_X, 2)));
rep_mean = repmat(a, [1, size(celeb_X,2)]);

T = (celeb_X - rep_mean);

temp = T'*T;

num_eigfaces = 20;
[V, D] = eigs(temp,num_eigfaces);

dimensions = T*V;

eig_faces = dimensions(:, end-num_eigfaces+1:end);


eig_faces = [];
figure(counter);
counter = counter + 1;
for i = 1:num_eigfaces
    eface = dimensions(:,i);
    eface = eface + a;
    min_val = min(eface);
    max_val = max(eface);
    eface = (eface - min_val)./(max_val - min_val);
    temp_eface = zeros(330,280);
    temp_eface(unmasked_pixels) = eface;
    eig_faces = [eig_faces, eface];
    
    if i <=10
        subplot(3,4, i);
        imshow(mat2gray(temp_eface));
    end
end
l2_errors = zeros(1,10);
l2_error = 0;
celeb_choices = randperm(size(celeb_X,2));
celeb_choices = celeb_choices(1:5);
num_faces = 5

figure(counter);
counter = counter + 1;
for num_vects = 1:10
    for j = 1:num_faces
        w{j} = linsolve(eig_faces(:,1:num_vects), celeb_X(:,celeb_choices(j)));
        temp_eface = zeros(330,280);
        temp_eface(unmasked_pixels) =  eig_faces(:,1:num_vects) * w{j};
        orig_face = zeros(330,280);
        orig_face(unmasked_pixels) = celeb_X(:,celeb_choices(j));
        l2_error = l2_error +  norm((eig_faces(:,1:num_vects) * w{j}) - celeb_X(:,celeb_choices(j)));
        subplot(2,num_faces,j);
        imshow(mat2gray(temp_eface));
        subplot(2,num_faces,j + num_faces);
        imshow(mat2gray(orig_face));
    end
    l2_errors(num_vects) = l2_error/num_faces;
    l2_error = 0;
end

figure(counter);
counter = counter + 1;
plot([1:10], l2_errors);
xlabel('Number of eigenvectors');
ylabel('L2 error');
title(['Plot of average L2 error on ' , num2str(num_faces) , ' celebrity faces']);



l2_errors = zeros(1,10);
l2_error = 0;

figure(counter);
counter= counter + 1;

student_choices = randperm(size(student_X,2));
student_choices = student_choices(1:5);

for num_vects = 1:20
    for j = 1:num_faces
        w{j} = linsolve(eig_faces(:,1:num_vects), student_X(:,student_choices(j)));
        temp_eface = zeros(330,280);
        temp_eface(unmasked_pixels) =  eig_faces(:,1:num_vects) * w{j};
        orig_face = zeros(330,280);
        orig_face(unmasked_pixels) = student_X(:,student_choices(j));
        l2_error = l2_error +  norm(eig_faces(:,1:num_vects) * w{j} - student_X(:,student_choices(j)));
        subplot(2,num_faces,j);
        imshow(mat2gray(temp_eface));
        subplot(2,num_faces,j + num_faces);
        imshow(mat2gray(orig_face));
    end
    l2_errors(num_vects) = l2_error / num_faces;
    l2_error = 0;
end

figure(counter);
counter = counter + 1;
plot([1:20], l2_errors);
xlabel('Number of eigenvectors');
ylabel('L2 error');
title(['Plot of average L2 error on ' , num2str(num_faces) , ' student faces']);
