function [out] = k_means()

[train_small_features, train_small_labels, train_features, train_labels, test_features, test_labels] = load_MNIST;
cluster_list = [5,10,20];
mean_set = cell(1, length(cluster_list));
clusters = cell(1,length(cluster_list));

for i = 1:length(cluster_list)
    [mean_set{i},clusters{i}] = EM(cluster_list(i), train_small_features{7}, train_small_labels{7});
    
end

for i = 1:length(mean_set)
    figure();
    for j = 1:length(mean_set{i})
        img = reshape( mean_set{i}{j}, [28 28]);
        subplot(length(mean_set{i})/5, 5, j);
        imshow(img);
    end
end

end

function [centers, clusters] = EM(num_clusters, x_large, y_large)
centers = cell(1,num_clusters);
clusters = cell(1,num_clusters);
for x = 1: length(clusters)
    clusters{x} = [];
end
set = randperm(size(x_large,2));

for i = 1:num_clusters
    %centers{i} = randi(255, [784,1]);
    centers{i} = x_large(:, set(i));
end
min = Inf;
min_id = 0;
fprintf('Initializing %d clusters for data set of size %d...\n', num_clusters, size(x_large,2)); 
for j = 1:size(x_large,2)
    for i = 1:num_clusters
        curr = sqrt(sum(double(x_large(:,j)) - double(centers{i})).^2);
        if curr < min
            min = curr;
            min_id = i;
        end
    end
    clusters{min_id} = [clusters{min_id}, x_large(:,j)];
end

new_centers = centers;

disp('Running E and M step till convergence...');

while 1
    for x = 1: num_clusters
        if mean(clusters{x},2)
            new_centers{x} = mean(clusters{x},2);
        end
    end
    if isequal(new_centers, centers)
        break;
    end
    
    min = Inf;
    min_id = 0;
    clusters = cell(1,num_clusters);
    for y = 1:size(x_large,2)
        for z = 1:num_clusters
            curr = sqrt(sum(double(x_large(:,y)) - double(new_centers{z})).^2);
            if curr < min
                min = curr;
                min_id = z;
            end
        end
        clusters{min_id} = [clusters{min_id}, x_large(:,y)];
    end
    centers = new_centers;
end

end

function [train_small_features, train_small_labels, train_features, train_labels, test_features, test_labels] = load_MNIST()
train_small_data = load('data/train_small.mat');
train_data = load('data/train.mat');
test_data = load('data/test.mat');

train_small_features = cell(1, length(train_small_data.train));
train_small_labels = cell(1, length(train_small_data.train));
for i = 1: length(train_small_data.train)
    train_small_features{i} = reshape(train_small_data.train{i}.images, [784, size(train_small_data.train{i}.images,3)]);
    train_small_labels{i} = train_small_data.train{i}.labels;
end

train_features = reshape(train_data.train.images, [784, size(train_data.train.images,3)]);
train_labels = train_data.train.labels;

test_features = reshape(test_data.test.images, [784, size(test_data.test.images,3)]);
test_labels = test_data.test.labels;
end