cel_dir = dir('CelebrityDatabase/*.jpg');
stud_dir = dir('StudentDatabase/*.jpg');
celebs_raw = cell(1, length(cel_dir));
students_raw = cell(1,length(stud_dir));

celeb_X = [];
student_X = [];

mask = load('mask.mat');
mask = mask.mask;

unmasked_pixels = find(mask);
masked_pixels = find(~mask);


for i = 1: length(cel_dir)
    celebs_raw{i} = (imread(['CelebrityDatabase/' cel_dir(i).name]));
    im_vector = celebs_raw{i}(unmasked_pixels);
    celebs_raw{i}(masked_pixels) = 0;
%     celebs_raw{i}= zeros(size(celebs_raw{i}));
%     celebs_raw{i}(unmasked_pixels) = im_vector;
    celebs_raw{i} = rgb2gray(celebs_raw{i});
    imshow(celebs_raw{i})
    celeb_X = [celeb_X, reshape(celebs_raw{i}, [size(celebs_raw{i},1) * size(celebs_raw{i},2), 1])];
end

size(celeb_X)

raw = celeb_X(:,1);
size(raw)
reshaped = reshape(raw, [330,280]);